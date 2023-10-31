part of 'season_management_cubit.dart';

class SeasonManagementState extends Equatable {
  LoadStatus? loadStatus;
  List<SeasonEntity>? seasonList;

  @override
  List<dynamic> get props => [
        loadStatus,
        seasonList,
      ];

  SeasonManagementState({
    this.loadStatus,
    this.seasonList,
  });

  SeasonManagementState copyWith({
    LoadStatus? loadStatus,
    List<SeasonEntity>? seasonList,
  }) {
    return SeasonManagementState(
      loadStatus: loadStatus ?? this.loadStatus,
      seasonList: seasonList ?? this.seasonList,
    );
  }
}
