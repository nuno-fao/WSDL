const category_items = document.getElementsByClassName("category-item");
const category_hidden_input = document.getElementById("category_input");
const category_dropdown = document.getElementById("categoryDropdown");
if (category_items) {
  for (const categoryItem of category_items) {
    categoryItem.addEventListener("click", () => {
      category_hidden_input.value = categoryItem.dataset.category;
      category_dropdown.innerText = categoryItem.dataset.category;
    });
  }
}
