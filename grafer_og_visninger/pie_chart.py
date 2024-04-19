import matplotlib.pyplot as plt


# Function to format the text to be displayed on the slices
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return f'{pct:.1f}%\n({val:d})'
    return my_autopct

def enkel_pie_chart(katekorier, verdier, tittel, farger=None):
    # Find the index of the highest value in sizes
    max_index = verdier.index(max(verdier))

    # Create an explode list with 0.0 for each item except for the maximum one
    explode = [0.1 if i == max_index else 0 for i in range(len(verdier))]
    farger = farger if farger is not None else ['#FF7F50', '#008080', '#9DC183', '#CDA4DE',
                                                '#87CEEB']  # Coral, Teal, Sage Green, Soft Violet, Sky Blue

    # Create the pie chart
    plt.figure(figsize=(4, 4), dpi=80)
    plt.pie(verdier, explode=explode, labels=katekorier, colors=farger, autopct=make_autopct(verdier),
            shadow=True, startangle=90)
    plt.axis('equal')  # Ensures the pie chart is drawn as a circle.
    plt.title(tittel)
    plt.show()


# Function to plot side-by-side pie charts
def side_ved_side_pie_chart(kategorier, verdi_foer, verdi_etter, tittel):
    farger = ['#FF7F50', '#008080', '#9DC183', '#CDA4DE', '#87CEEB']  # Coral, Teal, Sage Green, Soft Violet, Sky Blue

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].pie(verdi_foer, labels=kategorier, autopct=make_autopct(verdi_foer), startangle=75, colors=farger)
    axes[0].set_title(f'{tittel} \nFØR ENDRING')
    axes[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    axes[1].pie(verdi_etter, labels=kategorier, autopct=make_autopct(verdi_etter), startangle=75, colors=farger)
    axes[1].set_title(f'{tittel} \nETTER ENDRING')
    axes[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()