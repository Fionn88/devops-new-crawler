from src.main import crawl


def test_scrape_data():
    result, if_loop = crawl(1, False)

    # Check that result is a list
    assert isinstance(result, list), "Result should be a list"
    assert isinstance(if_loop, bool), "Result should be a bool"

    # Check that each item in the result is also a list
    for item in result:
        assert isinstance(
            item, list
            ), "Each item in the result should be a list"

        assert len(item) == 6, "Each item should have exactly 6 elements"

    for item in result:
        id_value, subject_value, tags_value, date_value, \
            author_value, link_value = item

        assert len(
            str(id_value)
            ) <= 300, "ID should not exceed 300 characters"
        assert len(
            str(subject_value)
            ) <= 200, "Subject should not exceed 200 characters"
        assert len(
            str(tags_value)
            ) <= 700, "Tags should not exceed 700 characters"
        assert len(
            str(author_value)
            ) <= 50, "Author should not exceed 50 characters"
        assert len(
            str(link_value)
            ) <= 200, "Link should not exceed 200 characters"

        assert isinstance(id_value, str), "ID should be an str"
        assert isinstance(subject_value, str), "Subject should be a string"
        assert isinstance(tags_value, str), "Tags should be a string"
        assert isinstance(date_value, str), "Date should be a string"
        assert isinstance(author_value, str), "Author should be a string"
        assert isinstance(link_value, str), "Link should be a string"
