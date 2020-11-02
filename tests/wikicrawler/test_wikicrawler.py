from wikicrawler import WikiCrawler


def test_main_noargs(mocker):
    mocker.patch.object(WikiCrawler, "explore_existing")
    args = "python app.py".split(" ")
    wikicrawler.start(args)
    wikicrawler.start.assert_called_once_with(args)