import 'dart:io';

import 'package:flutter_base/utils/logger.dart';
import 'package:image_picker/image_picker.dart';
import 'package:multi_image_picker/multi_image_picker.dart';
import 'package:uuid/uuid.dart';

class AttachFileHelper {
  AttachFileHelper._privateConstructor();

  static final AttachFileHelper shared = AttachFileHelper._privateConstructor();

  Future<List<Asset>> getListImageFromLibrary(
      {required bool enableCamera}) async {
    List<Asset> resultList = [];
    String error;

    try {
      resultList = await MultiImagePicker.pickImages(
        maxImages: 100,
        enableCamera: enableCamera,
      );
    } on Exception catch (e) {
      error = e.toString();
    }

    return resultList;
  }

  Future<File?> getImageFromLibrary() async {
    File? image;
    try {
      final picker = ImagePicker();
      final pickedFile = await picker.pickImage(source: ImageSource.gallery);
      if (pickedFile != null) {
        image = File(pickedFile.path);
      } else {
        logger.d('No image selected.');
      }
    } on Exception catch (e) {
      String error = e.toString();
    }
    return image;
  }

  Future<File?> getPictureByCamera() async {
    final picker = ImagePicker();
    File? image;
    try {
      var resultList = await picker.pickImage(source: ImageSource.camera);
      //đã bỏ image quality
      if (resultList != null) {
        image = File(resultList.path);
      } else {
        logger.d('No image selected.');
      }
    } on Exception catch (e) {
      String error = e.toString();
    }
    return image;
  }

  // Future<List<AttachFile>> get imageFromLibrary async {
  //   List<AttachFile> attachFiles = [];
  //
  //   File? attachFile = await getImageFromLibrary();
  //
  //   if (attachFile == null) return [];
  //
  //   /// size của file... tạm thời chưa cần
  //   var uuid = Uuid();
  //   var id = uuid.v1();
  //
  //   /// cần biết file upload có param như nào mới đóng gói dc trong đoạn này
  //   AttachFile file = AttachFile(
  //     id: id,
  //     file: File(attachFile.path),
  //     name: attachFile.path.split("/").last,
  //     mime: getMimeType(attachFile.path.split("/").last),
  //   );
  //   attachFiles.add(file);
  //
  //   return attachFiles;
  // }
  //
  // Future<List<AttachFile>> get imageFromCamera async {
  //   List<AttachFile> attachFiles = [];
  //
  //   File? cameraPickers = await getPictureByCamera();
  //
  //   if (cameraPickers == null) return [];
  //
  //   /// size của file... tạm thời chưa cần
  //   //int countSize = event.countSize ?? 0;
  //
  //   // cấp cho nó 1 cái id nào đó để dễ xử lý
  //   var uuid = Uuid();
  //   var id = uuid.v1();
  //
  //   /// cần biết file upload có param như nào mới đóng gói dc trong đoạn này
  //   AttachFile file = AttachFile(
  //     id: id,
  //     path: cameraPickers.path,
  //     file: cameraPickers,
  //     mime: getMimeType(cameraPickers.path.split("/").last),
  //     name: cameraPickers.path.split("/").last,
  //   );
  //   attachFiles.add(file);
  //
  //   return attachFiles;
  // }

  String getMimeType(String name) {
    if (equalsIgnoreCase(name, ".pdf"))
      return "application/pdf";
    else if (equalsIgnoreCase(name, ".doc"))
      return "application/msword";
    else if (equalsIgnoreCase(name, ".docx"))
      return "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
    else if (equalsIgnoreCase(name, ".xls"))
      return "application/vnd.ms-excel";
    else if (equalsIgnoreCase(name, ".xlsx"))
      return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
    else if (equalsIgnoreCase(name, ".ppt"))
      return "application/vnd.ms-powerpoint";
    else if (equalsIgnoreCase(name, ".pptx"))
      return "application/vnd.openxmlformats-officedocument.presentationml.presentation";
    else if (equalsIgnoreCase(name, ".zip"))
      return "application/zip";
    else if (equalsIgnoreCase(name, ".rtf"))
      return "application/rtf";
    else if (equalsIgnoreCase(name, ".eps"))
      return "application/postscript";
    else if (equalsIgnoreCase(name, ".txt"))
      return "text/plain";
    else if (equalsIgnoreCase(name, ".m4v"))
      return "application/pdf";
    else if (equalsIgnoreCase(name, ".mp4"))
      return "video/x-m4v";
    else if (equalsIgnoreCase(name, ".psd"))
      return "image/x-photoshop";
    else if (equalsIgnoreCase(name, ".ai"))
      return "application/postscript";
    else if (equalsIgnoreCase(name, ".img"))
      return "application/octet-stream";
    else if (equalsIgnoreCase(name, ".svg"))
      return "image/svg+xml";
    else if (equalsIgnoreCase(name, ".bmp"))
      return "image/x-ms-bmp";
    else if (equalsIgnoreCase(name, ".png"))
      return "image/png";
    else if (equalsIgnoreCase(name, ".jpg"))
      return "image/jpeg";
    else if (equalsIgnoreCase(name, ".jpeg"))
      return "image/jpeg";
    else if (equalsIgnoreCase(name, ".gif"))
      return "image/gif";
    else if (equalsIgnoreCase(name, ".heic"))
      return "image/heic";
    else if (equalsIgnoreCase(name, ".heif")) return "image/heif";
    return "";
  }

  bool equalsIgnoreCase(String string1, String string2) {
    return string1.toLowerCase().contains(string2.toLowerCase());
  }
}
