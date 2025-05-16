def process_intervals(user_intervals, l_start, l_end):
    """Обрабатывает интервалы времени пользователя (ученика или учителя).
    Разбивает входной список на пары (вход/выход), сортирует их по времени входа,
    объединяет пересекающиеся или смежные интервалы и обрезает их по границам урока."""
    pairs = []
    for i in range(0, len(user_intervals), 2):
        start = user_intervals[i]
        end = user_intervals[i + 1]
        pairs.append((start, end))
    sorted_pairs = sorted(pairs, key=lambda x: x[0])

    merged = []
    for s, e in sorted_pairs:
        if not merged:
            merged.append([s, e])
        else:
            _, last_e = merged[-1]
            if s <= last_e:
                merged[-1][1] = max(last_e, e)
            else:
                merged.append([s, e])

    clipped = []
    for s, e in merged:
        clipped_s = max(s, l_start)
        clipped_e = min(e, l_end)
        if clipped_s < clipped_e:
            clipped.append((clipped_s, clipped_e))

    return clipped


def appearance(intervals: dict[str, list[int]]) -> int:
    """Вычисляет общее время одновременного присутствия ученика и учителя на уроке.
    Обрабатывает интервалы урока, ученика и учителя, находит пересечения интервалов
    присутствия ученика и учителя (с учетом границ урока) и суммирует длительности этих пересечений.
    """
    lesson = intervals["lesson"]
    lesson_start, lesson_end = lesson[0], lesson[1]

    pupil = process_intervals(intervals["pupil"], lesson_start, lesson_end)
    tutor = process_intervals(intervals["tutor"], lesson_start, lesson_end)

    i = j = 0
    total = 0
    while i < len(pupil) and j < len(tutor):
        p_start, p_end = pupil[i]
        t_start, t_end = tutor[j]

        overlap_start = max(p_start, t_start)
        overlap_end = min(p_end, t_end)

        if overlap_start < overlap_end:
            total += overlap_end - overlap_start
            if p_end < t_end:
                i += 1
            else:
                j += 1
        else:
            if p_end < t_end:
                i += 1
            else:
                j += 1
    return total


# Тесты
tests = [
    {
        "intervals": {
            "lesson": [1594663200, 1594666800],
            "pupil": [
                1594663340,
                1594663389,
                1594663390,
                1594663395,
                1594663396,
                1594666472,
            ],
            "tutor": [1594663290, 1594663430, 1594663443, 1594666473],
        },
        "answer": 3117,
    },
    {
        "intervals": {
            "lesson": [1594702800, 1594706400],
            "pupil": [
                1594702789,
                1594704500,
                1594702807,
                1594704542,
                1594704512,
                1594704513,
                1594704564,
                1594705150,
                1594704581,
                1594704582,
                1594704734,
                1594705009,
                1594705095,
                1594705096,
                1594705106,
                1594706480,
                1594705158,
                1594705773,
                1594705849,
                1594706480,
                1594706500,
                1594706875,
                1594706502,
                1594706503,
                1594706524,
                1594706524,
                1594706579,
                1594706641,
            ],
            "tutor": [
                1594700035,
                1594700364,
                1594702749,
                1594705148,
                1594705149,
                1594706463,
            ],
        },
        "answer": 3577,
    },
    {
        "intervals": {
            "lesson": [1594692000, 1594695600],
            "pupil": [1594692033, 1594696347],
            "tutor": [1594692017, 1594692066, 1594692068, 1594696341],
        },
        "answer": 3565,
    },
]

if __name__ == "__main__":
    for i, test in enumerate(tests, start=1):
        test_answer = appearance(test["intervals"])
        assert (
            test_answer == test["answer"]
        ), f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
