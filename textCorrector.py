import re
from nltk.metrics import edit_distance
import enchant
import pprint
from deepmultilingualpunctuation import PunctuationModel

# from autocorrect import Speller

# spell = Speller(lang='en')


# Input text with numbering and bullet points
input_text = """
RFID:
1. RFID refers to Radio Frequency Identification.
2. It consists of a tag that is
of an integrated circuit and
made up
an antenna.
3. Another important module of the system is
the reader.
4. The tag (also known as transponder) is
attached to the object that is being identified.
5. The reader queries the tag be by sending
Radio Frequency (RF) waves to identify it.
6. RFIDs are made using multiple frequencies,
namely; low frequency, high frequency,
ultra high frequency, microwaves frequency, etc
7. Low frequency (LF) RFIDS were deployed
first for high-value, short-range industrial
appliances and car immobilizer.
8. Low frequency REID, have low data ranges
and low data rates.
9. High frequency RFIDs have high data rates
and longer data ranges.
10. Ultra High frequency RFIDs have even higher
data = ranges and data rates but they cannot
be used near metallic objects, water and
human bodies.
11. Principle of RFID:
voltage
A copper coll of is attached to a power sources
and due to the impedance it experiences,
a voltage is developed accross its terminals.
We can attach a capacitor parallel to this
coil to increase its voltage. We will call
this the primary coil. Now, we bring another
copper coil near the primary coll. This is the
secondary coil. The secondary coil experiences.
an emf from the primary coill and hence,
a voltage developed accross its terminals.
We connect a load resistor to thesecondary coil and current starts
I to flow in the secondary coil. This
flow of current results in the primary
coll experiencing a back emf
(electromotive
force). This is how wt we can see
find what device is attached to the
secondary coll, by measuring the voltage
across the primary coil.
Primary
Secondary
vis
Transformer
Fulll
Load
resistor
12. Applications of RFID in IOT !
a) Fast Tags.
: Government uses RFIDs to attached
to cars in order to pay tolls, instead
of the old way by stopping
b] Libraries : Books are attached with RFIDS
to make it easier to keep and inventory
e of books and to find their information
easily.
c} Identification & Tracking: RFIDs can be
attached to animals in order to keep
track of them.
"""


class textCorrector:
    def __init__(self, dict_name="en_GB", max_dist=2):
        # self.spell_dict = enchant.Dict(dict_name)
        # self.spell_dict = enchant.DictWithPWL("en_GB", "custom_dict.txt")
        # self.max_dist = max_dist
        self.model = PunctuationModel()
        # self.spell_dict = Speller(lang='en')

    def replace(self, word):
        if self.spell_dict.check(word):
            return word
        suggestions = self.spell_dict.suggest(word)

        if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
            return suggestions[0]
        else:
            return word
        # return self.spell_dict(word)

    def replace_in_string(self, input_string):
        input_string = re.sub(r"(\d+\.|\w\)|\w\}|\w])\s*", "", input_string)
        output_string = input_string
        # for word in input_string.split():
        #     output_string += self.replace(word) + " "
        output_string = self.model.restore_punctuation(output_string)
        return output_string.strip()


# Remove numbering and bullet points
# if __name__ == "__main__":
#     replacer =  textCorrector()
#     corrected_string = replacer.replace_in_string(input_text)
#     pprint.pprint(corrected_string)

# print(output_text)
