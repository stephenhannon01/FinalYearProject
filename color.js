var data = [{
  "Food.Group": "Vegetable", "Food": "White Corn - 1 Cup", "Calorie Count": 606
}, {
  "Food.Group": "Vegetable",
  "Food": "Broccoli - 1 Cup",
  "Calorie Count": 31
}, {
  "Food.Group": "Meat",
  "Food": "Pork - 100g",
  "Calorie Count": 242
}, {
  "Food.Group": "Grains",
  "Food": "Oats - 100g",
  "Calorie Count": 389
}];

var attributes = [{
  "Food": "White Corn - 1 Cup",
  "Hex": 200
}, {
  "Food": "Broccoli - 1 Cup",
  "Hex": 31
}, {
  "Food": "Pork - 100g",
  "Hex": 242
}, {
  "Food": "Oats - 100g",
  "Hex": 389
}];

var visualization = d3plus.viz()
  .container("#tree_map")
  .data(data)
  .type("tree_map")
  .resize(true)
  .id(["Food", "Food.Group"])
  .size("Calorie Count")
  .depth(0)
  .attrs(attributes)
  .color("Hex")
  .draw()
