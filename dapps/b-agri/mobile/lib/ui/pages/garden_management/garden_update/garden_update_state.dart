part of 'garden_update_cubit.dart';

class GardenUpdateState extends Equatable {
  String? name;
  String? area;
  String? managerId;
  LoadStatus? detailGardenStatus;
  GardenItemEntity? gardenData;
  LoadStatus? editGardenStatus;

  @override
  List<Object?> get props => [
        this.name,
        this.area,
        this.managerId,
        this.gardenData,
        this.detailGardenStatus,
        this.editGardenStatus,
      ];

  GardenUpdateState({
    this.name,
    this.area,
    this.managerId,
    this.detailGardenStatus,
    this.gardenData,
    this.editGardenStatus,
  });

  GardenUpdateState copyWith({
    String? name,
    String? area,
    String? managerId,
    LoadStatus? detailGardenStatus,
    GardenItemEntity? gardenData,
    LoadStatus? editGardenStatus,
  }) {
    return GardenUpdateState(
      name: name ?? this.name,
      area: area ?? this.area,
      managerId: managerId ?? this.managerId,
      detailGardenStatus: detailGardenStatus ?? this.detailGardenStatus,
      gardenData: gardenData ?? this.gardenData,
      editGardenStatus: editGardenStatus ?? this.editGardenStatus,
    );
  }
}
