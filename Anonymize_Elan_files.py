import os
import pympi
import pandas as pd

#Functions
def filter_tiers(tier_names, prefix_list):
    """Filter tiers based on a list of prefixes."""
    return [tier for tier in tier_names if any(tier.startswith(prefix) for prefix in prefix_list)]

def get_names_anonymize(filename, matched_sentences, tiers_to_getnames, tiers_to_anonymize, tiers_to_check):
    #Getting Names
    global global_names_list
    
    name_annotations = []
    
    for annotation in eaf.get_annotation_data_for_tier(tiers_to_getnames[0]):
        start_time, end_time, label, content = annotation
        if label and "name" in label.lower():
            name_annotations.append((start_time, end_time, content))

    eng_annotations = eaf.get_annotation_data_for_tier(tiers_to_getnames[1])

    for name_start, name_end, name_content in name_annotations:
        for eng_start, eng_end, eng_label, eng_content in eng_annotations:
            if eng_start <= name_end and eng_end >= name_start:
                matched_sentences.append({
                    "File_Name" : filename,
                    "Name (Noun)": name_content,
                    "Original_Sentence": eng_content,
                    "English_Sentence": eng_label
                })
                break

    #Ananomyzing Names
    for tier in tiers_to_anonymize:
        for name_start, name_end, name_content in name_annotations:
            if tier in tiers_to_check:  
                for name_start, name_end, name_content in name_annotations:
                    annotations = eaf.tiers[tier][0]  
                    for annotation_id, annotation_data in list(annotations.items()):
                        start_time = eaf.timeslots[annotation_data[0]]  # Start time
                        end_time = eaf.timeslots[annotation_data[1]]    # End time
                        content = annotation_data[2]                   # Annotation content

                        if name_content in content:
                            new_value = content.replace(name_content, "[ANONYMIZED]")

                            # Update annotation tuple
                            annotations[annotation_id] = (
                                annotation_data[0],  # start_time_slot_id
                                annotation_data[1],  # end_time_slot_id
                                new_value,           # annotation_value
                                annotation_data[3] if len(annotation_data) > 3 else None  # optional_svg_ref
                            )

                            eaf.add_annotation(tier, start_time, end_time, new_value)
            else:  
                annotations = eaf.tiers[tier][1]  
                for annotation_id, annotation_data in list(annotations.items()):
                    ref_annotation_id = annotation_data[0]  # Referenced annotation ID
                    content = annotation_data[1]           # Annotation content

                    if name_content in content:
                        new_value = content.replace(name_content, "[ANONYMIZED]")

                        # Update annotation tuple
                        annotations[annotation_id] = (
                            ref_annotation_id,  # referenced_annotation_id
                            new_value,          # anonymized content
                            annotation_data[2],  # optional metadata
                            annotation_data[3],  # optional metadata
                        )       

    eaf.to_file("Anonymized_Elan_files/"+os.path.splitext(filename)[0]+"_anonymized"+".eaf")


if __name__ == "__main__":
    input_folder = "Original_Elan_files"  # Original files
    output_folder = "Anonymized_Elan_files"
    os.makedirs(output_folder, exist_ok=True)
    matched_sentences = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".eaf"):  # Only process ELAN files
            file_path = os.path.join(input_folder, file_name)
            eaf = pympi.Elan.Eaf(file_path)

            # Extract all tier names from the ELAN file
            tier_names = eaf.get_tier_names()

            # Find tiers based on prefixes
            prefixes = ["Lemma@", "Words@", "Text@", "Gloss@", "PoS@", "engTrans@"]

            tiers_to_anonymize = filter_tiers(tier_names, prefixes)
            tiers_to_getnames = filter_tiers(tier_names, ["PoS@", "engTrans@"])
            tiers_to_check = filter_tiers(tier_names, ["Text@", "Words@"])


            get_names_anonymize(file_name, matched_sentences, tiers_to_getnames, tiers_to_anonymize, tiers_to_check)


    df = pd.DataFrame(matched_sentences)
    df.to_csv("Names_List.csv", encoding="utf-8", index=False)

    # Remove the .bak files
    for filename in os.listdir(output_folder):
        if filename.endswith(".bak"):
            file_path = os.path.join(output_folder, filename)
            os.remove(file_path)

    print("Data has been saved to 'Names_List.csv' and ELAN files are anonymized - saved in 'Anonymized_Elan_files' folder.")
