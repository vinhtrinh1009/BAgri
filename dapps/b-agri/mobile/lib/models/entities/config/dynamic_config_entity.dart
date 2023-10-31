import 'package:json_annotation/json_annotation.dart';

// DataFlow: Step 1 + 2
// Create entity
// Generate code : flutter pub run build_runner build --delete-conflicting-outputs
import 'item_config_entity.dart';
part 'dynamic_config_entity.g.dart';

@JsonSerializable()
class DynamicConfigEntity {
  @JsonKey()
  String? appName;
  @JsonKey()
  String? screenName;
  @JsonKey()
  String? section;
  @JsonKey()
  String? functionName;

  @JsonKey()
  String? id;

  @JsonKey()
  ItemConfigEntity? configuration;

  DynamicConfigEntity({
    this.appName,
    this.screenName,
    this.section,
    this.functionName,
    this.id,
    this.configuration,
  });

  DynamicConfigEntity copyWith({
    String? appName,
    String? screenName,
    String? section,
    String? functionName,
    String? id,
    String? configuration,
  }) {
    return new DynamicConfigEntity(
        appName: appName ?? this.appName,
        screenName: screenName ?? this.screenName,
        section: section ?? this.section,
        functionName: functionName ?? this.functionName,
        id: id ?? this.id,
        configuration: configuration as ItemConfigEntity? ?? this.configuration);
  }

  factory DynamicConfigEntity.fromJson(Map<String, dynamic> json) => _$DynamicConfigEntityFromJson(json);
  
  Map<String, dynamic> toJson() => _$DynamicConfigEntityToJson(this);
}
