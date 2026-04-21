from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = "topfive_secret_key"  # Added secret key to enable flash messages

# Simple in-memory storage for submissions
submissions = []

@app.route("/", methods=["GET", "POST"])
def home():
    global submissions
    if request.method == "POST":
        # Get the category and top five items from the form
        category = request.form.get("category", "").strip()
        items = [
            request.form.get(f"item{i}", "").strip() for i in range(1, 6)
        ]

        # Improved validation with user-friendly error messages
        if not category:
            flash("⚠️ Please enter a category.", "error")
            return redirect("/")
        
        if not all(items):
            flash("⚠️ Please fill in all five items.", "error")
            return redirect("/")

        # Check for duplicate categories (case-insensitive)
        existing_categories = [s["category"].lower() for s in submissions]
        if category.lower() in existing_categories:
            flash(f"⚠️ A Top Five list for '{category}' already exists!", "error")
            return redirect("/")

        submissions.append({"category": category, "five": items})
        flash(f"✅ Your Top Five '{category}' list was submitted!", "success")
        return redirect("/")

    return render_template("index.html", submissions=submissions)


# Added a new route to delete a submission by index
@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    global submissions
    if 0 <= index < len(submissions):
        removed = submissions.pop(index)
        flash(f"🗑️ Deleted your Top Five '{removed['category']}' list.", "success")
    else:
        flash("⚠️ Could not find that submission.", "error")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
