from latex import measure_latex_dimensions, render_latex_and_show



def main():
    # diagram: Final = Diagram(
    #     Imperative(r"Eingabe: \texttt{n}")
    # )
    # print(diagram.emit())

    print(measure_latex_dimensions("Hello, world!"))
    render_latex_and_show(r"Hello, world! $\frac{1}{2} \cdot \texttt{GEIER!!!}$")


if __name__ == "__main__":
    main()
