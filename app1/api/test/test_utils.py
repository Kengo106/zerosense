from django.test import TestCase, SimpleTestCase
from ..utils import judge_hit


class TestUtils(SimpleTestCase):
    def test_judge_hit(self):
        #  tan,fuku1,wide13
        votes = [1, 5, 3]
        expected = [True, True, False, False, False,
                    False, False, True, False, False, False]
        self.assertEqual(judge_hit(votes), expected)

        #  null
        votes = [8, 5, 1]
        expected = [False, False, False, False, False,
                    False, False, False, False, False, False]
        self.assertEqual(judge_hit(votes), expected)

        # fuku2, umaren, wide12
        votes = [2, 1, 6]
        expected = [False, False, True, False, True,
                    False, True, False, False, False, False]
        self.assertEqual(judge_hit(votes), expected)

        # fuku3, wide13
        votes = [3, 5, 1]
        expected = [False, False, False, True, False,
                    False, False, True, False, False, False]
        self.assertEqual(judge_hit(votes), expected)

        # fuku3, umaren, wide12, wide13, wide23, trio
        votes = [3, 2, 1]
        expected = [False, False, False, True, True,
                    False, True, True, True, True, False]
        self.assertEqual(judge_hit(votes), expected)

        #  tan,fuku1,umaren,umatan,wide12,
        votes = [1, 2, 9]
        expected = [True, True, False, False, True,
                    True, True, False, False, False, False]
        self.assertEqual(judge_hit(votes), expected)

    '''
    scores = [tan,fuku1,fuku2,fuku3,umaren,umatan,wide12,wide13,wide23,trio,teirce]

    単勝（vote[0]）
    複勝（vote[0]）
    馬連（vote[0],vote[1]）
    馬連（vote[0],vote[2]）
    馬連（vote[1],vote[2]）
    馬単（vote[0]-vote[1]）
    ワイド（vote[0],vote[1]）
    ワイド（vote[0],vote[2]）
    ワイド（vote[1],vote[2]）
    三連複（vote[0],vote[1],vote[2]）
    三連単（vote[0]-vote[1]-vote[2]）

    単勝:1着以内に入る馬、1頭選べ（1着の着順）
    複勝:3着以内に入る馬、1頭選べ
    馬連:2着以内に入る馬、2頭選べ
    馬単:1着,2着の着順
    ワイド:3着以内に入る馬、2頭選べ
    三連複:3着以内に入る馬、3頭選べ
    三連単:1着,2着,3着の着順

    '''
