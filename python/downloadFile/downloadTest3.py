import urllib.request
import os

def downloadMethod():

    url = ('http://115.157.63.60/v4.music' +
     '.126.net/20170222062937/882e203d86106868e7f04c1' +
     'de4b03eb4/web/cloudmusic/MGA0ISAwITA2MCEhJCAwIA' +
     '==/mv/207097/4398046579975_1280x720.mp4')

    fileName = os.path.basename(url)

    print("开始下载文件:" + fileName)

    urllib.request.urlretrieve(url, fileName, progressBar)


def progressBar(blockNum, blockSize, totalSize):
    '''
    blockNum:下载了的文件模块个数
    blockSize:每个模块的大小
    totalSize:文件的总大小
    '''

    alreadyDownloadSize = blockNum * blockSize
    percent = (alreadyDownloadSize / totalSize) * 100

    if percent > 100:
        percent = 100

    print('--->' + '%.2f%%' % percent + '---' +
          "%.2f"%(alreadyDownloadSize/1024/1024) + 'Mb/'
          + "%.2f"%(totalSize/1024/1024) + 'Mb')

    if percent == 100:
        print("下载完成")


if __name__ == '__main__':
    downloadMethod()
