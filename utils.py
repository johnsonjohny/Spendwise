
def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount (₹): ").strip())

            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                return amount

        except ValueError:
            print("Invalid amount. Please enter a number.")


def parse_tags(tag_input):
    tags = {
        tag.strip().lower()
        for tag in tag_input.split(",")
        if tag.strip()
    }

    return tags
