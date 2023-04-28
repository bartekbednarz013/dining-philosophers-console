# Ucztujący filozofowie - aplikacja konsolowa
Aplikacja konsolowa dla systemu Windows implementująca rozwiązanie klasycznego problemu synchronizacji procesów.

Jednak tym razem nasi filozofowie podczas jedzenia czytają, a uczta kończy się, gdy wszyscy filozofowie przeczytają wszystkie dostępne książki. Nad przebiegiem uczty czuwa kelner, który dopuszcza do stołu maksymalnie czterech (spośród pięciu obecnych) gości jednocześnie. Najpierw każdy filozof losowo wybiera książkę, której jeszcze nie czytał, a gdy zostanie dopuszczony do stołu, losowo wybiera miejsce. Po zajęciu miejsca próbuje zdobyć widelce, a następnie je i czyta. Gdy skończy jeść, wstaje od stołu, odkłada książkę i wybiera następną, chyba że przeczytał już wszystkie - wtedy opuszcza ucztę.

Dostępne są dwie implementacje: wielowątkowa i wieloprocesowa.

Użytkownik wybiera implementację, a następnie wprowadza liczbę książek, jakie mają przeczytać filozofowie. Następnie wyświetlany jest cały przebieg uczty.
