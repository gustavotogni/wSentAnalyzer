import matplotlib.pyplot as plt
import squarify
from nltk import FreqDist

class wPlotter:

    def __init__(self, outputPath):
        self.counter = 0
        self.outputPath = outputPath

    def mkFileName(self, title):
        self.counter = self.counter + 1
        return self.outputPath + '%02d' % self.counter + "_" + title + ".png"   

    def mpsTreeMap(self, values, title, dataset):
    
        df = values.groupby('sentiment').size().reset_index(name='counts')

        labels = df.apply(lambda x: str(x[0]) + "\n (" + str(x[1]) + ")", axis=1)
        sizes = df['counts'].values.tolist()
        colors = [plt.cm.Spectral(i/float(len(labels))) for i in range(len(labels))]
        
        plt.figure(figsize=(12,8), dpi= 80)        
        squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)
        plt.title(title + " " + dataset)
        plt.axis('off')
        plt.savefig(self.mkFileName("mps" + dataset))        
        plt.close()

    def fdistCumulative(self, values, title, dataset):

        allContents = []
        for wordList in values['tokens']:
            allContents += wordList    

        fdist1 = FreqDist(allContents)
        
        plt.ion()
        fdist1.plot(25, cumulative=False, title = title + " " + dataset)
        plt.tight_layout()
        plt.savefig(self.mkFileName("wfdist" + dataset))  
        plt.ioff()
        plt.close()

    def fdistByGroup(self, values, title, dataset):
        
        for index, row in values.iterrows():
            fdist1 = FreqDist(row['tokens'])
            plt.ion()
            fdist1.plot(25, cumulative=False, title=(title + " (" + index + ") " + dataset))
            plt.tight_layout()

            plt.savefig(self.mkFileName("wfdist" + dataset + " " + index))
            plt.ioff()
            plt.close()