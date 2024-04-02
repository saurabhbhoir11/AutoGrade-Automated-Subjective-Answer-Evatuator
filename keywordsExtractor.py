import yake

# saved_dir = "USE"
# use_model = tf.saved_model.load(saved_dir)
#
# kw_model = KeyBERT(use_model)
#
# paragraph2 = (
#     "APPLICATION AREAS OF COMPUTER VISION "
#     "HEALTHCARE - A well-known area of application of computer vision "
#     "is in healthcare. For example, ultrasound has found use in many areas that previously used X-ray or "
#     "other techniques.  Accompanying this progress is the greatly increased use of computer vision "
#     "techniques in medical imaging. Application of computer vision in medical imaging is a challenging task "
#     "because of the complexity of medical images.  Medical images are processed and interpreted to extract "
#     "a variety of data for diagnosis of the medical condition. These include tumor detection, "
#     "malign changes, organ dimensions, blood flow in vessels, and much additional vital information.  It "
#     "is evident that effective use of computer vision in medical image processing can provide valuable "
#     "information for diagnosis and treatment. "
#     "MILITARY - Another significant use of computer vision is in "
#     "military applications.  Automatic target recognition is one of the important applications of vision "
#     "technology wherein images are automatically interpreted and analyzed to identify potential targets. "
#     "This can help improve the speed and accuracy of target identification and elimination.  Missile "
#     "control management is another area where computer vision systems help to identify specific targets "
#     "accurately to facilitate automated guidance of missiles.  More advanced systems for missile guidance "
#     "send the missile to an area rather than a specific target, and target selection is made when the "
#     "missile reaches the area based on locally acquired image data.  Modern military concepts, "
#     "such as “battlefield awareness,” imply that various sensors, including image sensors, provide a rich "
#     "set of information about a combat scene which can be used to support strategic decisions. "
#     "AUTOMATION - "
#     "Another emerging application area is in autonomous control of vehicles. Autonomous vehicles include "
#     "submersibles; land-based vehicles like cars, trucks, and small robots with wheels; and aerial vehicles "
#     "and unmanned aerial vehicles (UAVs).  Computer vision helps the driver or pilot in navigating the "
#     "vehicles and automates many tasks such as application of brakes, steering control, obstacle detection, "
#     "etc.  Autonomous vehicles can also be applied to specific tasks like locating and putting down forest "
#     "fires, self-directed landing of aircraft, speed control, collision prevention, and many more such "
#     "applications.  Several car manufacturers have demonstrated systems for autonomous driving of cars and "
#     "such vehicles may soon become available in the commercial market. "
#     "FOOD INDUSTRY - Computer vision is "
#     "becoming increasingly important is in the food industry, where over the last two decades, "
#     "image processing has been rapidly diffused as an instrument for automatic food quality evaluation and "
#     "control.  Most food products have a heterogeneous matrix, therefore, their appearance properties ("
#     "color, texture, shape, and size) can be strongly variable, even within the same product category.  "
#     "Computer vision systems can effectively replace visual inspection in different applications such as "
#     "harvesting, quality control, sorting and grading, portioning, and label verification.  Furthermore, "
#     "they provide a more objective and standard evaluation of food quality parameters over a large number "
#     "of samples."
#     "OTHER AREAS - Computer vision is also being applied to OCR. For example, handwritten postal "
#     "codes on letters can be read and automatically sorted based on address and routing destinations.  "
#     "Automatic number plate recognition (ANPR) is another important application that would help to identify "
#     "vehicles for collecting money at toll stations as well as to aid law enforcement agencies in tracking "
#     "movement of vehicles.  Computer vision technology is beginning to find a place in many consumer "
#     "products, including camera phones, interfaces to games consoles, parking and driving assistance in "
#     "automobiles, computer/internet image and video searches, and more recently internet shopping.  It "
#     "also finds application in retail for 3D model building. Visual authentication is another area of "
#     "interest where computer vision can be used to automatically detect faces of humans."
# )
# paragraph1 = (
#     "APPLICATION AREAS OF COMPUTER VISION : "
#     "Other : The versatility of computer vision extends to Optical Character "
#     "Recognition (OCR), where handwritten postal codes on letters are deciphered, enabling automated sorting based on "
#     "addresses and routing destinations.A crucial application is Automatic Number Plate Recognition (ANPR), "
#     "aiding in the identification of vehicles for toll collection and assisting law enforcement agencies in "
#     "monitoring vehicle movements. The integration of computer vision into consumer products is on the rise, "
#     "ranging from camera phones and gaming console interfaces to parking and driving assistance in automobiles. "
#     "Additionally, it plays a role in computer and internet image and video searches, as well as more recent "
#     "applications in internet shopping. In the realm of retail, computer vision contributes to 3D model building, "
#     "enhancing the visual representation of products. Visual authentication emerges as an area of interest, "
#     "with computer vision employed to automatically detect human faces, offering applications in security and "
#     "authentication systems."
#     "Food Industry : An escalating trend in significance is witnessed as computer "
#     "vision plays an increasingly pivotal role in the food industry. Over the past two decades, image processing has "
#     "rapidly permeated the industry, serving as a valuable tool for the automatic evaluation and control of food "
#     "quality. The intrinsic diversity of most food products, characterized by a heterogeneous matrix, necessitates "
#     "advanced technologies. Properties like color, texture, shape, and size can exhibit considerable variation even "
#     "within the same product category. Computer vision systems emerge as powerful substitutes for visual inspection "
#     "across various applications in the food industry. From harvesting and quality control to sorting and grading, "
#     "portioning, and label verification, these systems streamline processes, ensuring efficiency and precision. "
#     "Beyond efficiency gains, computer vision brings objectivity and standardization to the evaluation of food "
#     "quality parameters. This is particularly valuable when dealing with a large number of samples, providing a "
#     "reliable and consistent assessment of food quality across diverse scenarios."
#     "Healthcare : Computer vision plays a pivotal role in the healthcare sector, with one notable "
#     "application being in medical imaging. Ultrasound, for instance, has emerged as a versatile tool, "
#     "replacing traditional techniques like X-rays in various medical fields. The continuous advancement in "
#     "this domain is paralleled by the widespread adoption of computer vision techniques in medical imaging. "
#     "The intricacy of medical images poses a significant challenge, making the application of computer "
#     "vision in this context particularly demanding. Extracting meaningful data from medical images is "
#     "crucial for diagnosis and treatment. Computer vision contributes to this process by processing and "
#     "interpreting medical images, facilitating tasks such as tumor detection, identification of malignant "
#     "changes, measurement of organ dimensions, assessment of blood flow in vessels, and the extraction of "
#     "other vital information. The integration of computer vision into medical image processing holds the "
#     "promise of delivering valuable insights for effective diagnosis and treatment. It is evident that "
#     "harnessing the power of computer vision in healthcare can significantly enhance the quality of medical "
#     "information available to healthcare professionals. Military: Computer vision holds considerable "
#     "significance in military applications, serving diverse purposes in enhancing operational efficiency. "
#     "An integral facet is the utilization of computer vision in automatic target recognition, "
#     "a pivotal technology that automatically interprets and analyzes images to identify potential targets. "
#     "This advancement contributes significantly to expediting target identification and elimination with "
#     "heightened precision. In missile control management, computer vision systems play a vital role in "
#     "accurately identifying specific targets. This aids in the automated guidance of missiles, ensuring a "
#     "more targeted and effective approach. Advancements in missile guidance systems have led to more "
#     "sophisticated approaches. Some systems direct missiles to a designated area rather than a precise "
#     "target. Target selection occurs upon reaching the area, based on locally acquired image data. "
#     'Embracing modern military concepts, such as "battlefield awareness," involves leveraging various '
#     "sensors, including image sensors. These sensors provide a comprehensive dataset about a combat scene, "
#     "supporting strategic decisions by furnishing crucial information to military commanders. Automation : "
#     "A burgeoning field for applications of computer vision is found in the autonomous control of a diverse "
#     "range of vehicles. This encompasses submersibles, land-based vehicles such as cars, trucks, "
#     "and wheeled robots, as well as aerial vehicles and unmanned aerial vehicles (UAVs).The integration of "
#     "computer vision technology in autonomous vehicles is transformative. It assists drivers or pilots in "
#     "navigation while automating critical tasks like brake application, steering control, and obstacle "
#     "detection, thereby enhancing overall vehicle autonomy. Beyond conventional transportation, autonomous "
#     "vehicles find application in specialized tasks such as firefighting, self-directed aircraft landings, "
#     "speed control, collision prevention, and various other scenarios where automation proves beneficial. "
#     "Notably, several leading car manufacturers have showcased systems for autonomous driving, signaling a "
#     "shift towards the imminent availability of such vehicles in the commercial market. The prospect of "
#     "autonomous vehicles is poised to redefine transportation norms in the near future. "
# )

# kw1 = kw_model.extract_keywords(paragraph1, keyphrase_ngram_range=(0, 3), top_n=20, diversity=0.8)
# kw2 = kw_model.extract_keywords(paragraph2, keyphrase_ngram_range=(0, 3), top_n=20, diversity=0.8)

# kw_extractor = yake.KeywordExtractor()
#
# kw1 = kw_extractor.extract_keywords(paragraph1)
# kw2 = kw_extractor.extract_keywords(paragraph2)
#
# # Extract unique lowercase keywords
# keywords1 = set(i[0].lower() for i in kw1)
# keywords2 = set(i[0].lower() for i in kw2)
#
# # Find common keywords
# common_keywords = keywords1.intersection(keywords2)
#
# # Print the results
# print("Keywords from Yake:")
# print("Keywords in paragraph 1:", keywords1)
# print("Keywords in paragraph 2:", keywords2)
# print("Common Keywords:", common_keywords)
#

class keyWords:
    def __init__(self):
        # self.kw_model = KeyBERT(use_model)
        self.kw_model = yake.KeywordExtractor()

    def extract_keywords(self, paragraph1, answer, question):
        # kw1 = self.kw_model.extract_keywords(
        #     self.paragraph1, keyphrase_ngram_range=(0, 3), top_n=20, diversity=0.8
        # )
        # kw2 = self.kw_model.extract_keywords(
        #     self.paragraph2, keyphrase_ngram_range=(0, 3), top_n=20, diversity=0.8
        # )
        paragraph1 = paragraph1.lower()
        count = 0
        for phrase in answer:
            if phrase in paragraph1:
                count += 1
        if question in ["2A", "2B", "3A", "3B"]:
            score = count / 10
            if score > 1:
                score = 1
        else:
            score = count / 5
            if score > 1:
                score = 1
        return score

    def get_keywords(self, paragraph):
        # kw = self.kw_model.extract_keywords(
        #     paragraph, keyphrase_ngram_range=(0, 3), top_n=20, diversity=0.8
        # )
        kw = self.kw_model.extract_keywords(paragraph)
        kw = [i[0].lower() for i in kw]
        return kw
