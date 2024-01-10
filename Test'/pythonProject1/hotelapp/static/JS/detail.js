function displayImages() {
  var imageContainer = document.getElementById("image-container");
  var imageCountInput = document.getElementById("image-count-input");
  var imageCount = parseInt(imageCountInput.value);

  // Xóa các ảnh cũ trong container (nếu có)
  imageContainer.innerHTML = "";

  // Tạo và thêm các ảnh mới vào container
  for (var i = 1; i <= imageCount; i++) {
    var imageElement = document.createElement("img");
    imageElement.src = "path/to/your/image" + i + ".jpg"; // Thay đổi đường dẫn tương ứng với tên ảnh của bạn
    imageContainer.appendChild(imageElement);
  }
}