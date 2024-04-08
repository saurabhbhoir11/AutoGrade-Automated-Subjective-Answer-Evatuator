import tensorflow as tf
import numpy as np


# use_model = tf.saved_model.load(saved_dir)
# r = Rake()

paragraph2 = (
    "APPLICATION AREAS OF COMPUTER VISION "
    "HEALTHCARE - A well-known area of application of computer vision "
    "is in healthcare. For example, ultrasound has found use in many areas that previously used X-ray or "
    "other techniques.  Accompanying this progress is the greatly increased use of computer vision "
    "techniques in medical imaging. Application of computer vision in medical imaging is a challenging task "
    "because of the complexity of medical images.  Medical images are processed and interpreted to extract "
    "a variety of data for diagnosis of the medical condition. These include tumor detection, "
    "malign changes, organ dimensions, blood flow in vessels, and much additional vital information.  It "
    "is evident that effective use of computer vision in medical image processing can provide valuable "
    "information for diagnosis and treatment. "
    "MILITARY - Another significant use of computer vision is in "
    "military applications.  Automatic target recognition is one of the important applications of vision "
    "technology wherein images are automatically interpreted and analyzed to identify potential targets. "
    "This can help improve the speed and accuracy of target identification and elimination.  Missile "
    "control management is another area where computer vision systems help to identify specific targets "
    "accurately to facilitate automated guidance of missiles.  More advanced systems for missile guidance "
    "send the missile to an area rather than a specific target, and target selection is made when the "
    "missile reaches the area based on locally acquired image data.  Modern military concepts, "
    "such as “battlefield awareness,” imply that various sensors, including image sensors, provide a rich "
    "set of information about a combat scene which can be used to support strategic decisions. "
    "AUTOMATION - "
    "Another emerging application area is in autonomous control of vehicles. Autonomous vehicles include "
    "submersibles; land-based vehicles like cars, trucks, and small robots with wheels; and aerial vehicles "
    "and unmanned aerial vehicles (UAVs).  Computer vision helps the driver or pilot in navigating the "
    "vehicles and automates many tasks such as application of brakes, steering control, obstacle detection, "
    "etc.  Autonomous vehicles can also be applied to specific tasks like locating and putting down forest "
    "fires, self-directed landing of aircraft, speed control, collision prevention, and many more such "
    "applications.  Several car manufacturers have demonstrated systems for autonomous driving of cars and "
    "such vehicles may soon become available in the commercial market. "
    "FOOD INDUSTRY - Computer vision is "
    "becoming increasingly important is in the food industry, where over the last two decades, "
    "image processing has been rapidly diffused as an instrument for automatic food quality evaluation and "
    "control.  Most food products have a heterogeneous matrix, therefore, their appearance properties ("
    "color, texture, shape, and size) can be strongly variable, even within the same product category.  "
    "Computer vision systems can effectively replace visual inspection in different applications such as "
    "harvesting, quality control, sorting and grading, portioning, and label verification.  Furthermore, "
    "they provide a more objective and standard evaluation of food quality parameters over a large number "
    "of samples."
    "OTHER AREAS - Computer vision is also being applied to OCR. For example, handwritten postal "
    "codes on letters can be read and automatically sorted based on address and routing destinations.  "
    "Automatic number plate recognition (ANPR) is another important application that would help to identify "
    "vehicles for collecting money at toll stations as well as to aid law enforcement agencies in tracking "
    "movement of vehicles.  Computer vision technology is beginning to find a place in many consumer "
    "products, including camera phones, interfaces to games consoles, parking and driving assistance in "
    "automobiles, computer/internet image and video searches, and more recently internet shopping.  It "
    "also finds application in retail for 3D model building. Visual authentication is another area of "
    "interest where computer vision can be used to automatically detect faces of humans."
)
paragraph1 = (
    "APPLICATION AREAS OF COMPUTER VISION : "
    "Other : The versatility of computer vision extends to Optical Character "
    "Recognition (OCR), where handwritten postal codes on letters are deciphered, enabling automated sorting based on "
    "addresses and routing destinations.A crucial application is Automatic Number Plate Recognition (ANPR), "
    "aiding in the identification of vehicles for toll collection and assisting law enforcement agencies in "
    "monitoring vehicle movements. The integration of computer vision into consumer products is on the rise, "
    "ranging from camera phones and gaming console interfaces to parking and driving assistance in automobiles. "
    "Additionally, it plays a role in computer and internet image and video searches, as well as more recent "
    "applications in internet shopping. In the realm of retail, computer vision contributes to 3D model building, "
    "enhancing the visual representation of products. Visual authentication emerges as an area of interest, "
    "with computer vision employed to automatically detect human faces, offering applications in security and "
    "authentication systems."
    "Food Industry : An escalating trend in significance is witnessed as computer "
    "vision plays an increasingly pivotal role in the food industry. Over the past two decades, image processing has "
    "rapidly permeated the industry, serving as a valuable tool for the automatic evaluation and control of food "
    "quality. The intrinsic diversity of most food products, characterized by a heterogeneous matrix, necessitates "
    "advanced technologies. Properties like color, texture, shape, and size can exhibit considerable variation even "
    "within the same product category. Computer vision systems emerge as powerful substitutes for visual inspection "
    "across various applications in the food industry. From harvesting and quality control to sorting and grading, "
    "portioning, and label verification, these systems streamline processes, ensuring efficiency and precision. "
    "Beyond efficiency gains, computer vision brings objectivity and standardization to the evaluation of food "
    "quality parameters. This is particularly valuable when dealing with a large number of samples, providing a "
    "reliable and consistent assessment of food quality across diverse scenarios."
    "Healthcare : Computer vision plays a pivotal role in the healthcare sector, with one notable "
    "application being in medical imaging. Ultrasound, for instance, has emerged as a versatile tool, "
    "replacing traditional techniques like X-rays in various medical fields. The continuous advancement in "
    "this domain is paralleled by the widespread adoption of computer vision techniques in medical imaging. "
    "The intricacy of medical images poses a significant challenge, making the application of computer "
    "vision in this context particularly demanding. Extracting meaningful data from medical images is "
    "crucial for diagnosis and treatment. Computer vision contributes to this process by processing and "
    "interpreting medical images, facilitating tasks such as tumor detection, identification of malignant "
    "changes, measurement of organ dimensions, assessment of blood flow in vessels, and the extraction of "
    "other vital information. The integration of computer vision into medical image processing holds the "
    "promise of delivering valuable insights for effective diagnosis and treatment. It is evident that "
    "harnessing the power of computer vision in healthcare can significantly enhance the quality of medical "
    "information available to healthcare professionals. Military: Computer vision holds considerable "
    "significance in military applications, serving diverse purposes in enhancing operational efficiency. "
    "An integral facet is the utilization of computer vision in automatic target recognition, "
    "a pivotal technology that automatically interprets and analyzes images to identify potential targets. "
    "This advancement contributes significantly to expediting target identification and elimination with "
    "heightened precision. In missile control management, computer vision systems play a vital role in "
    "accurately identifying specific targets. This aids in the automated guidance of missiles, ensuring a "
    "more targeted and effective approach. Advancements in missile guidance systems have led to more "
    "sophisticated approaches. Some systems direct missiles to a designated area rather than a precise "
    "target. Target selection occurs upon reaching the area, based on locally acquired image data. "
    'Embracing modern military concepts, such as "battlefield awareness," involves leveraging various '
    "sensors, including image sensors. These sensors provide a comprehensive dataset about a combat scene, "
    "supporting strategic decisions by furnishing crucial information to military commanders. Automation : "
    "A burgeoning field for applications of computer vision is found in the autonomous control of a diverse "
    "range of vehicles. This encompasses submersibles, land-based vehicles such as cars, trucks, "
    "and wheeled robots, as well as aerial vehicles and unmanned aerial vehicles (UAVs).The integration of "
    "computer vision technology in autonomous vehicles is transformative. It assists drivers or pilots in "
    "navigation while automating critical tasks like brake application, steering control, and obstacle "
    "detection, thereby enhancing overall vehicle autonomy. Beyond conventional transportation, autonomous "
    "vehicles find application in specialized tasks such as firefighting, self-directed aircraft landings, "
    "speed control, collision prevention, and various other scenarios where automation proves beneficial. "
    "Notably, several leading car manufacturers have showcased systems for autonomous driving, signaling a "
    "shift towards the imminent availability of such vehicles in the commercial market. The prospect of "
    "autonomous vehicles is poised to redefine transportation norms in the near future. "
)
# Replace
# with actual sentences

# Combine all sentences into a single list
# all_sentences = paragraph1 + paragraph2

# Get embeddings for all sentences
# embeddings = use_model(all_sentences)

# Separate embeddings for each paragraph

# embeddings_paragraph1 = embeddings[:len(paragraph1)]
# embeddings_paragraph2 = embeddings[len(paragraph1):]
#
# # Calculate cosine similarity between each sentence in paragraph1 and every sentence in paragraph2
# similarity_matrix = tf.linalg.matmul(
#     tf.math.l2_normalize(embeddings_paragraph1, axis=1),
#     tf.math.l2_normalize(embeddings_paragraph2, axis=1),
#     transpose_b=True
# )
#
# # Display the similarity matrix
# print("Similarity Matrix:")
# print(similarity_matrix.numpy())
#
# max_similarity_scores = tf.reduce_max(similarity_matrix, axis=1).numpy()
# print("Maximum Similarity Scores for Each Sentence in Paragraph1:")
# print(max_similarity_scores)

# paragraph1_sentences = [
#     sentence.strip() for sentence in paragraph1.split(".") if sentence
# ]
# paragraph2_sentences = [
#     sentence.strip() for sentence in paragraph2.split(".") if sentence
# ]
#
# print(len(paragraph1_sentences))
# print(len(paragraph2_sentences))
#
# # Initialize an array to store similarity scores
# similarity_scores = np.zeros((len(paragraph1_sentences), len(paragraph2_sentences)))
#
# # Calculate similarity scores
# for i, sentence1 in enumerate(paragraph1_sentences):
#     for j, sentence2 in enumerate(paragraph2_sentences):
#         sentence1_embedding = use_model([sentence1])[0]
#         sentence2_embedding = use_model([sentence2])[0]
#         similarity_scores[i, j] = np.inner(
#             sentence1_embedding, sentence2_embedding
#         ).flatten()[0]
#
# # Display similarity scores for i, sentence1 in enumerate(paragraph1_sentences): for j, sentence2 in enumerate(
# # paragraph2_sentences): print(f"Similarity Score between Sentence {i + 1} in Paragraph 1 and Sentence {j + 1} in
# # Paragraph 2: {similarity_scores[i, j]:.4f}")
#
# kw1 = r.extract_keywords_from_text(paragraph1)
# kw2 = r.extract_keywords_from_text(paragraph2)
#
# print(similarity_scores)
#
# max_values = np.max(similarity_scores, axis=1)
# max_indices = np.argmax(similarity_scores, axis=1)
#
# # Display the results
# for i, (max_val, max_idx) in enumerate(zip(max_values, max_indices)):
#     print(f"Row {i + 1}: Max Value = {max_val}, Max Index = {max_idx}")
#
# set = set()
#
# for i, (max_val, max_idx) in enumerate(zip(max_values, max_indices)):
#     if max_val > 0.5:
#         set.add(max_idx)
#
#
# print(set)
# print(len(set))
# score = len(set) / len(paragraph2_sentences)
# print(score)


class USE:
    def __init__(self, *args, **kwargs):
        saved_dir = "USE"
        if args:
            self.paragraph1 = args[0]
            self.paragraph2 = args[1]
        self.use_model = tf.saved_model.load(saved_dir)

    def get_similarity_score(self, paragraph1, paragraph2, question):
        dataset = []
        paragraph1_sentences = [
            sentence.strip() for sentence in paragraph1.split(".") if sentence
        ]
        paragraph2_sentences = [
            sentence.strip() for sentence in paragraph2.split(".") if sentence
        ]

        similarity_scores = np.zeros(
            (len(paragraph1_sentences), len(paragraph2_sentences))
        )

        for i, sentence1 in enumerate(paragraph1_sentences):
            for j, sentence2 in enumerate(paragraph2_sentences):
                sentence1_embedding = self.use_model([sentence1])[0]
                sentence2_embedding = self.use_model([sentence2])[0]
                similarity_scores[i, j] = np.inner(
                    sentence1_embedding, sentence2_embedding
                ).flatten()[0]

        max_values = np.max(similarity_scores, axis=1)
        max_indices = np.argmax(similarity_scores, axis=1)

        for i, (max_val, max_idx) in enumerate(zip(max_values, max_indices)):
            if max_val > 0.35:
                dataset.append(max_idx)
        # print(question)
        # print(dataset)
        print(f"Length of dataset: {len(dataset)}, Length of paragraph1: {len(paragraph1_sentences)}")
        if (len(dataset) - len(paragraph1_sentences)) > 2:
            length = len(paragraph1_sentences)
        else:
            length = len(dataset)
        if question in ["2A", "2B", "3A", "3B"]:
            score = length / 15
            if score > 1:
                score = 1
        # elif question == "1A":
        #     score = length / 7
        #     print(f"2, {score}")
        #     if score > 1:
        #         score = 1
        else:
            score = length / 8
            if score > 1:
                score = 1
        return score, len(dataset), len(paragraph1_sentences)

    def get_embeddings(self, sentences):
        embeddings = self.use_model(sentences)
        return embeddings


# use = USE()
# print(use.get_similarity_score(paragraph1, paragraph2))
