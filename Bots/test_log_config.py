from log_config import split_text_on_parts


def test_split_text_on_parts_with_empty_text():
    text = ''
    parts = split_text_on_parts(text, 12)

    assert parts == []


def test_split_text_on_parts_with_short_text():
    text = 'Short text'
    parts = split_text_on_parts(text, 12)

    assert parts == [text]


def test_split_text_on_parts_with_long_text():
    text = 'Long enough text'
    parts = split_text_on_parts(text, 12)

    assert parts == [
        'Long enough ',
        'text',
    ]


def test_split_text_on_parts_with_very_long_text_with_line_break():
    text = 'Very long text that enough for\nfour parts'
    parts = split_text_on_parts(text, 12)

    assert parts == [
        'Very long te',
        'xt that enou',
        'gh for',
        'four parts',
    ]


def test_split_text_on_parts_with_long_text_with_two_line_breaks():
    text = 'Long\nenough\ntext'
    parts = split_text_on_parts(text, 7)

    assert parts == [
        'Long',
        'enough',
        'text',
    ]
