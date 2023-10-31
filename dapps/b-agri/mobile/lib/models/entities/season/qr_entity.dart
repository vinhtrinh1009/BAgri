import 'package:json_annotation/json_annotation.dart';

part 'qr_entity.g.dart';

@JsonSerializable()
class QREntity {
  String? qr_code_url;
  String? link;

  factory QREntity.fromJson(Map<String, dynamic> json) =>
      _$QREntityFromJson(json);
  Map<String, dynamic> toJson() => _$QREntityToJson(this);

  QREntity({
    this.qr_code_url,
    this.link,
  });

  QREntity copyWith({
    String? qr_code_url,
    String? link,
  }) {
    return QREntity(
      qr_code_url: qr_code_url ?? this.qr_code_url,
      link: link ?? this.link,
    );
  }
}
