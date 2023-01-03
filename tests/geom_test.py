import geom


class TestLineIntersection(object):
    def test_orthogonal_crossing_at_origin(self):
        expected = 0, 0
        actual = geom.line_intersection(line1=([-1, 0], [1, 0]), line2=([0, -1], [0, 1]))
        assert actual == expected
