part of 'season_adding_cubit.dart';

class SeasonAddingState extends Equatable {
  LoadStatus? loadStatus;
  String? seasonName;
  GardenEntity? gardenEntity;
  ProcessEntity? processEntity;
  TreeEntity? treeEntity;
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
        duration,
        processDetail,
      ];

  SeasonAddingState resetDuration({
    LoadStatus? loadStatus,
    String? seasonName,
    GardenEntity? gardenEntity,
    ProcessEntity? processEntity,
    TreeEntity? treeEntity,
    String? startTime,
    String? endTime,
    int? duration,
    ProcessEntity? processDetail,
  }) {
    return SeasonAddingState(
      loadStatus: loadStatus ?? this.loadStatus,
      seasonName: seasonName ?? this.seasonName,
      gardenEntity: gardenEntity ?? this.gardenEntity,
      processEntity: processEntity ?? this.processEntity,
      treeEntity: treeEntity ?? this.treeEntity,
      processDetail: processDetail ?? this.processDetail,
      startTime: startTime ?? this.startTime,
      endTime: endTime,
      duration: duration,
    );
  }

  SeasonAddingState({
    this.loadStatus,
    this.seasonName,
    this.gardenEntity,
    this.processEntity,
    this.treeEntity,
    this.startTime,
    this.endTime,
    this.duration,
    this.processDetail,
  });

  SeasonAddingState copyWith({
    LoadStatus? loadStatus,
    String? seasonName,
    GardenEntity? gardenEntity,
    ProcessEntity? processEntity,
    TreeEntity? treeEntity,
    String? startTime,
    String? endTime,
    int? duration,
    ProcessEntity? processDetail,
  }) {
    return SeasonAddingState(
        loadStatus: loadStatus ?? this.loadStatus,
        seasonName: seasonName ?? this.seasonName,
        gardenEntity: gardenEntity ?? this.gardenEntity,
        processEntity: processEntity ?? this.processEntity,
        treeEntity: treeEntity ?? this.treeEntity,
        startTime: startTime ?? this.startTime,
        endTime: endTime ?? this.endTime,
        duration: duration ?? this.duration,
        processDetail: processDetail ?? this.processDetail);
  }
}
