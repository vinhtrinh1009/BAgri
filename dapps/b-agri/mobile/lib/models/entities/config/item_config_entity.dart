import 'package:json_annotation/json_annotation.dart';

part 'item_config_entity.g.dart';

@JsonSerializable()
class ItemConfigEntity {
  @JsonKey()
  String? icon;
  @JsonKey()
  String? label;
  @JsonKey()
  int? order;
  @JsonKey()
  bool? isActive;
  bool? accessible;

  ItemConfigEntity({
    this.icon,
    this.label,
    this.order,
    this.isActive,
    this.accessible,
  });

  ItemConfigEntity copyWith({
    String? icon,
    String? label,
    String? order,
    String? isActive,
    String? accessible,
  }) {
    return new ItemConfigEntity(
      icon: icon ?? this.icon,
      label: label ?? this.label,
      order: order as int? ?? this.order,
      isActive: isActive as bool? ?? this.isActive,
      accessible: accessible as bool? ?? this.accessible,
    );
  }

  factory ItemConfigEntity.fromJson(Map<String, dynamic> json) => _$ItemConfigEntityFromJson(json);
  
  Map<String, dynamic> toJson() => _$ItemConfigEntityToJson(this);
}
