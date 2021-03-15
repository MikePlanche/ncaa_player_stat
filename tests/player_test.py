from second.stat_player import stat_player

def test_player():

    df = stat_player('https://www.sports-reference.com/cbb/players/larry-nance-2.html')

    assert df.shape==(5, 30)

