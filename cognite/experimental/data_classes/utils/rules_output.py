import copy

import regex


def _label_groups(extractors, conditions):
    colors = ["blue", "red", "green", "orange", "purple"]

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
                return f"<font color='{color}'>\\g<{group_counter}></font>"
            else:
                return f"\\g<{group_counter}>"

        extractor["restorePattern"] = regex.sub("\(.*?\)", color_group, extractor["pattern"].strip("$^"))

    return extractors


def _color_matches(extractors, matches):
    columns = [
        (source_target, field)
        for source_target in ["source", "target"]
        for field in sorted(list(matches[0][f"{source_target}KeyFields"].keys()))
    ]
    patterns = {
        (extractor["entitySet"][:-1], extractor["field"]): extractor["pattern"].strip("^$")
        for extractor in extractors
        if extractor["extractorType"] == "regex"
    }
    html = ""
    html += (
        "<table><tr>"  # Look mum I'm a frontend designer
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
            "source": copy.copy(match["sourceKeyFields"]),
            "target": copy.copy(match["targetKeyFields"]),
        }

        for extractor in extractors:
            if extractor["extractorType"] != "regex":
                continue
            source_target = extractor["entitySet"][:-1]  # singular
            field = extractor["field"]
            regex_match = regex.match(extractor["pattern"], match[f"{source_target}KeyFields"][field])
            if not regex_match:
                print(
                    "Unexpected lack of match of ",
                    extractor["pattern"],
                    match[f"{source_target}KeyFields"][field],
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
            + f"<td>{match['existingMatchType']}</td><td>{match['consistentMatch']}</td></tr>"
        )
    return html
