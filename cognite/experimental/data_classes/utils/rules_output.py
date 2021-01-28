import copy
from typing import Dict, List

import regex


def _label_groups(extractors: List[Dict], conditions: List[Dict]):
    colors = [
        "".join(f"{int(round(rgb*255)):02x}" for rgb in color)
        for color in [
            [0, 0.3470, 0.841],
            [0.9, 0.3250, 0.098],
            [0.9290, 0.694, 0.125],
            [0.4940, 0.184, 0.556],
            [0.4660, 0.674, 0.188],
            [0.3010, 0.745, 0.933],
            [0.6350, 0.078, 0.184],
        ]
    ]

    for extractor in extractors:
        extractor["groupLabel"] = {}

    for ci, condition in enumerate(conditions):
        if condition["conditionType"] != "equals":
            continue
        for ei, part in condition["arguments"]:
            extractor = extractors[ei]
            extractor["groupLabel"][part + 1] = ci  # 1-based

    for extractor in extractors:
        if extractor["extractorType"] != "regex":
            continue
        group_counter = 0

        def color_group(_):
            nonlocal group_counter, extractor
            group_counter += 1
            label_ix = extractor["groupLabel"].get(group_counter)
            if label_ix is not None:
                color = colors[label_ix % len(colors)]
                return f"<font color='#{color}'>\\g<{group_counter}></font>"
            else:
                return f"\\g<{group_counter}>"

        extractor["restorePattern"] = (
            "<font color='#666'>" + regex.sub(r"\(.*?\)", color_group, extractor["pattern"].strip("$^")) + "</font>"
        )

    return extractors


def _color_matches(extractors: List[Dict], matches: List[Dict]):
    columns = sorted(list({(extractor["entitySet"][:-1], extractor["field"]) for extractor in extractors}))  # order?
    patterns = {
        (extractor["entitySet"][:-1], extractor["field"]): extractor["pattern"].strip("^$")
        for extractor in extractors
        if extractor["extractorType"] == "regex"
    }
    html = ""
    html += (
        "<table><tr>"
        + "".join(
            f"<th style='text-align: center'><span style='font-size:150%'>{source_target}:{field}</span>"
            + f"<br>{patterns.get((source_target,field),'')}</th>"
            for source_target, field in columns
        )
        + "<th style='text-align: center'>Existing<br>Match Type</th>"
        + "<th style='text-align: center'>Consistent<br>Match?</th></tr>"
    )

    for match in matches:
        formatted = {
            "source": copy.copy(match.get("source")),
            "target": copy.copy(match.get("target")),
        }

        for extractor in extractors:
            if extractor["extractorType"] != "regex":
                continue
            source_target = extractor["entitySet"][:-1]  # singular
            field = extractor["field"]
            regex_match = regex.match(extractor["pattern"], match.get(source_target, {}).get(field, ""))
            if not regex_match:
                print(
                    "Unexpected lack of match of ", extractor["pattern"], match.get(source_target), field,
                )
                continue
            formatted_field = regex_match.expand(extractor["restorePattern"])
            formatted[source_target][field] = formatted_field

        html += (
            "<tr style='text-align: left'>"
            + "".join(
                f"<td style='text-align: left'>{formatted[source_target][field] }</td>"
                for source_target, field in columns
            )
            + f"<td>{match.get('existingMatchType')}</td><td>{match.get('consistentMatch')}</td></tr>"
        )
    return html
