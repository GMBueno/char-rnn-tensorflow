import mido
import os

class Music():
    def __init__(self, dataset, output = ""):
        ''' Using clip=True to clip velocity of notes to 127 if were higher. '''
        self.mids = []
        print('Starting...')
        # for each file in dataset folder, appends to self.mids
        for mid in os.listdir(dataset):
            # self.mids.append(mido.MidiFile(dataset+'/'+ mid, clip=True))
            self.mids.append(mido.MidiFile(dataset+'/'+ mid))
        print(f'--> there are {len(self.mids)} mid files in this dataset folder')
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
            mids = self.get_mid_without_meta_msgs()
            print('--> starting conversion to .txt...')
            total_lines = len(mids)
            curr_line = 1
            # percent and limit are used only to know progress percentage.
            percent = 0
            limit = 0
            for line in mids:
                # if there are 3 attributes aka time, note, and velocity
                if len(line) == 3:
                    time = str(line[0])
                    note = str(line[1])
                    vel = str(line[2])
                    file.write(f'{time} {note} {vel}')
                    if curr_line > limit:
                        print(f'----> conversion progress: {percent}%')
                        limit = int((percent/100)*total_lines)
                        percent += 10
                    if curr_line < total_lines:
                        file.write("\n")
                curr_line = curr_line + 1
            print('DONE!')

    ## WHEN TIME IS ACCESSED BY MID FILE, IT REPRESENTS SECONDS
    ## WHEN TIME IS ACCESSED BY TRACK, IT REPRESENTS TICKS
    def get_mid_without_meta_msgs(self):
        '''
        what:
        returns a big list generated from the mids. [time, note, vel]
        '''
        clean_mid = []
        tps = 50000
        current_mid = 1
        total_mids = len(self.mids)
        for mid in self.mids:
            print(f'----> reading mid {current_mid} of {total_mids}')
            for msg in mid:
                if msg.type == 'note_off' or msg.type =='note_on':
                    # clean_mid.append({'time': round(50_000*msg.time), 'note': msg.note, 'vel': msg.velocity})
                    clean_mid.append((round(tps*msg.time), msg.note, msg.velocity))
            current_mid += 1
        return clean_mid

dataset = 'datasets/input/2018maestro20files'
output = 'datasets/output/2018maestro20files.txt'
music = Music(dataset, output)
music.mid2text()
