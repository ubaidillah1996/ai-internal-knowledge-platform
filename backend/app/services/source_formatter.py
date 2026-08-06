def format_sources(results):

    grouped = {}


    for item in results:

        metadata = item.get("metadata", {})

        filename = metadata.get("filename")

        chunk_index = metadata.get("chunk_index")

        distance = item.get("distance")


        if filename not in grouped:

            grouped[filename] = {

                "filename": filename,

                "chunks": [],

                "best_distance": distance

            }


        grouped[filename]["chunks"].append(
            chunk_index
        )


        if distance < grouped[filename]["best_distance"]:

            grouped[filename]["best_distance"] = distance


    return list(grouped.values())