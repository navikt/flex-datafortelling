import matplotlib.pyplot as plt


def enkel_bar_chart(katekorier, verdier, tittel, farger=None):
    farger = farger if farger is not None else ['#FF7F50', '#008080']  # Coral and Teal
    # Create bar chart
    plt.figure(figsize=(8, 4))
    plt.bar(katekorier, verdier, color=farger, width=0.5)
    plt.xlabel('Svar')
    plt.ylabel('Antall')
    plt.title(tittel)
    plt.show()
