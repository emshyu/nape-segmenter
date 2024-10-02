import webvtt

class V0:
    # Takes in a list of words and stores them in a hash table
    def __init__(self, words):
        self.words = words
        self.hash_table = {}

        for word in self.words:
            key = word[0] 

            if key in self.hash_table:
                if word not in self.hash_table[key]:
                    self.hash_table[key].append(word)
            else:
                self.hash_table[key] = self.hash_table.setdefault(key, [word])


    # Takes in a txt file and writes to a txt new file
    # Whenever a "key word" is found, the file gets broken into a new line
    def segment_by_words (self, filename):
        with open(filename, 'r') as file:
            content = file.read()
            words = content.split()
            modified_content = []

            for word in words:
                key = word[0]

                if key in self.hash_table:
                    if word in self.hash_table[key]:
                        modified_content.append('\n' + word)
                    else:
                        modified_content.append(word)

            modified_text = ' '.join(modified_content)

            with open('modified_' + filename, 'w') as file:
                file.write(modified_text)

    # Takes in a VTT file and outputs a new properly segmented VTT file
    def segment_vtt (self, filename):
        # List of tuples (start_timestamp, end_timestamp, text)
        all_segments = []
        first_caption = webvtt.read(filename)[0]
        curr_segment = ['00:00:00.000', first_caption.end, first_caption.text]

        # Parse vtt file and stores segments into data structure
        for caption in webvtt.read(filename)[1:]:
            print(f'Time: {caption.start} --> {caption.end}')
            print(caption.text)
            print()  # Blank line for readability

            words = caption.text.split()
            found = False # Boolean to track if the segment contains a flagged word

            for word in words:
                key = word[0]

                # If the transcription segment contains a split word, start a new segment containing entire caption
                if key in self.hash_table:
                    if word in self.hash_table[key]:
                        found = True
                        break

            if found:
                curr_segment[1] = caption.start
                all_segments.append(curr_segment)
                curr_segment = [caption.start, caption.end, caption.text]
            else:
                curr_segment[1] = caption.start
                curr_segment[2] += " " + caption.text

        all_segments.append(curr_segment)

        # Making a new VTT file
        out_filename = 'modified_' + filename
        out_content = self.generate_vtt(all_segments)

        with open(out_filename, "w") as out_file:
            out_file.write(out_content)

    # Takes in a list of captions and generates a vtt
    def generate_vtt(self, captions):
        vtt_content = "WEBVTT\n\n"
        
        for index, [start, end, caption] in enumerate(captions, start=1):
            vtt_content += f"{index}\n"
            vtt_content += f"{start} --> {end}\n"
            vtt_content += f"{caption}\n\n"
        
        return vtt_content

    # Returns made hash table
    def get_hash_table(self):
        return self.hash_table

# Example usage
words = ["apple", "banana", "berry", "carrot", "cherry"]
tester = V0(words)

print(tester.get_hash_table())  # Output: {'apple': 0, 'banana': 1, 'cherry': 2}
tester.segment_by_words("test_file.txt")
tester.segment_vtt("sample.vtt")
