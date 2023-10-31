part of 'season_updating_cubit.dart';

class SeasonUpdatingState extends Equatable {
  LoadStatus? loadStatus;
  String? seasonName;
  GardenEntity? gardenEntity;
  ProcessEntity? processEntity;
  TreeEntity? treeEntity;
  SeasonEntity? seasonDetail;

  String? startTime;
  String? endTime;
  int? duration;

  ProcessEntity? processDetail;

  bool get buttonEnabled {
    if (seasonName == null ||
        startTime == null ||
        endTime == null ||
        gardenEntity == null ||
        processEntity == null ||
        treeEntity == null)
      return false;
    else if (seasonName!.isEmpty)
      return false;
    else
      return true;
  }

  @override
  List<dynamic> get props => [
        seasonName,
        gardenEntity,
        processEntity,
        treeEntity,
        startTime,
        endTime,
        loadStatus,
        seasonDetail,
        duration,
        processDetail,
      ];

  SeasonUpdatingState resetDuration({
    LoadStatus? loadStatus,
    String? seasonName,
    GardenEntity? gardenEntity,
    ProcessEntity? processEntity,
    TreeEntity? treeEntity,
    SeasonEntity? seasonDetail,
    String? startTime,
    String? endTime,
    int? duration,
    ProcessEntity? processDetail,
  }) {
    return SeasonUpdatingState(
      loadStatus: loadStatus ?? this.loadStatus,
      seasonName: seasonName ?? this.seasonName,
      gardenEntity: gardenEntity ?? this.gardenEntity,
      processEntity: processEntity ?? this.processEntity,
      treeEntity: treeEntity ?? this.treeEntity,
      seasonDetail: seasonDetail ?? this.seasonDetail,
      startTime: startTime ?? this.startTime,
      endTime: endTime,
      duration: duration,
      processDetail: processDetail ?? this.processDetail,
    );
  }

  SeasonUpdatingState({
    this.loadStatus,
    this.seasonName,
    this.gardenEntity,
    this.processEntity,
    this.treeEntity,
    this.seasonDetail,
    this.startTime,
    this.endTime,
    this.duration,
    this.processDetail,
  });

  SeasonUpdatingState copyWith({
    LoadStatus? loadStatus,
    String? seasonName,
    GardenEntity? gardenEntity,
    ProcessEntity? processEntity,
    TreeEntity? treeEntity,
    SeasonEntity? seasonDetail,
    String? startTime,
    String? endTime,
    int? duration,
    ProcessEntity? processDetail,
  }) {
    return SeasonUpdatingState(
      loadStatus: loadStatus ?? this.loadStatus,
      seasonName: seasonName ?? this.seasonName,
      gardenEntity: gardenEntity ?? this.gardenEntity,
      processEntity: processEntity ?? this.processEntity,
      treeEntity: treeEntity ?? this.treeEntity,
      seasonDetail: seasonDetail ?? this.seasonDetail,
      startTime: startTime ?? this.startTime,
      endTime: endTime ?? this.endTime,
      duration: duration ?? this.duration,
      processDetail: processDetail ?? this.processDetail,
    );
  }
}
