part of 'garden_list_by_qlv_cubit.dart';

class GardenListByQlvState extends Equatable {
  LoadStatus? getGardenStatus;
  List<GardenEntity>? listGardenData;

  GardenListByQlvState({this.getGardenStatus, this.listGardenData});

  GardenListByQlvState copyWith({
    LoadStatus? getGardenStatus,
    List<GardenEntity>? listGardenData,
  }) {
    return GardenListByQlvState(
      getGardenStatus: getGardenStatus ?? this.getGardenStatus,
      listGardenData: listGardenData ?? this.listGardenData,
    );
  }

  @override
  List<Object?> get props => [this.getGardenStatus, this.listGardenData];
}
