import urllib2


def getFileAs(fileName):
    url = "https://chemapps.stolaf.edu/jmol/jmol.php?get&pdbid=60C"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)

    with open(fileName, "w") as file:
        file.write(response.read())
