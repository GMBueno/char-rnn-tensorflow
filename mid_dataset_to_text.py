import mido
import os

class Music():
    def __init__(self, dataset, output = ""):
        ''' Using clip=True to clip velocity of notes to 127 if were higher. '''
        self.mids = []
        for mid in os.listdir(dataset):
            # self.mids.append(mido.MidiFile(dataset+'/'+ mid, clip=True))
            self.mids.append(mido.MidiFile(dataset+'/'+ mid))
        self.output = output

    def mid2text(self):
        '''
        what:
        writes the text file that represents all the musics together.
        how:
        opens new text file that will contain all the musics together
        calls func to get the list that represents all mids
        for each message in the clean mid
        get each attribute (time, note, velocity) in msg, writes them in file
        '''
        with open(self.output, "w+") as file:
            for item in self.get_mid_without_meta_msgs():
                for attr in item:
                    file.write(str(attr))
                    file.write(" ")
                file.write("\n")

    ## WHEN TIME IS ACCESSED BY MID FILE, IT REPRESENTS SECONDS
    ## WHEN TIME IS ACCESSED BY TRACK, IT REPRESENTS TICKS
    def get_mid_without_meta_msgs(self):
        '''
        what:
        returns a big list generated from the mids. [time, note, vel]
        '''
        clean_mid = []
        tps = 50000
        for mid in self.mids:
            for msg in mid:
                if msg.type == 'note_off' or msg.type =='note_on':
                    # clean_mid.append({'time': round(50_000*msg.time), 'note': msg.note, 'vel': msg.velocity})
                    clean_mid.append((round(tps*msg.time), msg.note, msg.velocity))
        return clean_mid

dataset = 'datasets/chiptune/'
output = 'datasets/chiptune/text.txt'
music = Music(dataset, output)
music.mid2text()
