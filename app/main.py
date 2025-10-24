from services.extraction import PDF

if __name__ == "__main__":
    pdf=PDF("samples/sampleJosh.pdf")
    option = input("Enter '1' to extract text or '2' to count pages: ")
    if option == '1':
        print("Extracted Text:")
        print(pdf.extract_text())
    elif option == '2':
        print(f"Number of pages: {pdf.count_pages()}")