import os

filenames = os.listdir()

for filename in filenames:
    if filename.startswith('AnXin'):
        #print(filename)
        mainfilename, extension = filename.split('.')
        powerstation, date, time = mainfilename.split('-')

        newfilename = 'demo_{}_{}.sqlite'.format(date, time)
        #print(newfilename)

        os.rename(filename, newfilename)
        
