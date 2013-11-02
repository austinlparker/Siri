from util import hook, http
from urllib import urlencode


def get_beer(inp):
    """ search beeradvocate.com """

    search_url = "http://beeradvocate.com/search"
    base_url = "http://beeradvocate.com"

    try:
        xfToken = http.get_html(base_url).xpath("//fieldset[@id='QuickSearch']/form[@class='formPopup']/input")[0].value
    except IndexError:
        return "Unable to retrieve token."

    post_dict = {
        'q' : inp,
        'qt' : 'beer',
        '_xfToken' : xfToken,
    }
    results = http.get_html(search_url, post_data=urlencode(post_dict))
    
    try:
        result = results.xpath("//div[@id='content']/div[@class='pageWidth']/div[@class='pageContent']/div[@class='mainContainer']/div[@class='mainContent']/fieldset/div[@id='baContent']/div[2]/ul/li[1]")[0]
    except IndexError:
        return "No Results"

    page_url = base_url + result.xpath('a')[0].get('href')
    scores = http.get_html(page_url).cssselect('.BAscore_big')
    beer_info = [x.text_content() for x in result.xpath('a')]

    return "%s by %s :: Community Score: %s :: Bros Score: %s :: %s" % (beer_info[0], 
                                                                        beer_info[1],
                                                                        scores[0].text_content(), 
                                                                        scores[1].text_content(), page_url)

@hook.command
def beeradvocate(inp):
    return get_beer(inp)

if __name__ == "__main__":
    print get_beer("Chimay")
