part of 'garden_list_cubit.dart';

class GardenListState extends Equatable {
  LoginStatusBagri? getGardenStatus;
  LoadStatus? deleteGardenStatus;
  List<GardenEntity>? listGardenData;

  GardenListState(
      {this.getGardenStatus, this.listGardenData, this.deleteGardenStatus});

  GardenListState copyWith({
    LoginStatusBagri? getGardenStatus,
    List<GardenEntity>? listGardenData,
    LoadStatus? deleteGardenStatus,
  }) {
    return GardenListState(
      getGardenStatus: getGardenStatus ?? this.getGardenStatus,
      listGardenData: listGardenData ?? this.listGardenData,
      deleteGardenStatus: deleteGardenStatus ?? this.deleteGardenStatus,
    );
  }

  @override
  List<Object?> get props =>
      [this.getGardenStatus, this.listGardenData, this.deleteGardenStatus];
}
