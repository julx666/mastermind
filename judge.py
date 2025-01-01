from collections import Counter

def check(k, hidden, query):
    #sprawdzanie poprawności wejścia
    if len(hidden) != len(query):
        raise ValueError("Długości sekwencji ukrutej i kodującej muszą być równe")

    if not all((1 <= x <= k) for x in hidden + query):
        raise ValueError("Liczby muszą należeć do przedziału od 1 do k(liczby dostępnych kolorów)")
    #liczenie pionków na właściwym miejscu
    correct_position_and_color = sum(h == q for h, q in zip(hidden, query)) #sprawdzamy czy elementy w parze są takie same

    #liczenie pionków o właściwym kolorze
    hidden_remaining = [h for h, q in zip(hidden, query) if h != q]
    query_remaining = [q for h, q in zip(hidden, query) if h != q]

    hidden_remaining = set(hidden_remaining)
    query_remaining = set(query_remaining)

    correct_color = 0
    for color in query_remaining:
        if color in hidden_remaining:
            correct_color += 1

    return correct_position_and_color, correct_color


hidden = [2,3,1,2]
query = [2,3,1,2]
print(check(4, hidden, query))