import 'package:flutter_base/models/entities/user/user_entity.dart';

class GlobalData {
  GlobalData._privateConstructor();

  static final GlobalData instance = GlobalData._privateConstructor();

  String? token;
  String? role;
  UserEntity? userEntity;
}
