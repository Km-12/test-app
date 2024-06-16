from models.models import AnswerExplanation


class AnswerCheck:

    FAILURE = "failure"
    NOT_ANSWERED = "not_answered"

    # 答えを確認する
    @staticmethod
    def answerslist_check(answer_list):
        checker_list = AnswerCheck.get_checker()
        incorrect = 0

        if answer_list and "" in answer_list:
            return AnswerCheck.NOT_ANSWERED, incorrect

        for i, ans in enumerate(answer_list):
            if ans != checker_list[i]:
                incorrect += 1
            if incorrect >= 2:
                return AnswerCheck.FAILURE, incorrect

        score = len(answer_list) - incorrect

        return "", score

    # 解答群の取得
    def get_checker():

        all_answer_explanation = AnswerExplanation.query.all()

        checker_list = []

        for answer_explanation in all_answer_explanation:

            checker_list.append(answer_explanation.answer)

        return checker_list
