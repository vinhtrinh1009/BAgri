part of 'garden_detail_cubit.dart';

class GardenDetailState extends Equatable {
  LoadStatus? getGardenStatus;
  GardenItemEntity? gardenData;

  GardenDetailState({
    this.getGardenStatus,
    this.gardenData,
  });

  GardenDetailState copyWith({
    LoadStatus? getGardenStatus,
    GardenItemEntity? gardenData,
  }) {
    return GardenDetailState(
      getGardenStatus: getGardenStatus ?? this.getGardenStatus,
      gardenData: gardenData ?? this.gardenData,
    );
  }

  @override
  List<Object?> get props => [
        this.getGardenStatus,
        this.gardenData,
      ];
}
