import 'package:json_annotation/json_annotation.dart';

part 'file_entity.g.dart';

@JsonSerializable()
class FileEntity {
  String? file_path;
  String? url;
  String? name;

  factory FileEntity.fromJson(Map<String, dynamic> json) =>
      _$FileEntityFromJson(json);

  Map<String, dynamic> toJson() => _$FileEntityToJson(this);

  FileEntity({
    this.file_path,
    this.url,
    this.name,
  });

  FileEntity copyWith({
    String? file_path,
    String? url,
    String? name,
  }) {
    return FileEntity(
      file_path: file_path ?? this.file_path,
      url: url ?? this.url,
      name: name ?? this.name,
    );
  }
}
