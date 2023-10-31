part of 'process_season_cubit.dart';

class ProcessSeasonState extends Equatable {
  final String? name;
  final LoadStatus? updateProcessSeasonStatus;
  final List<TreeEntity>? trees;
  final List<StageEntity>? stages;
  final LoadStatus? loadDetailStatus;
  int actionWithStepStatus;

  ProcessSeasonState({
    this.name,
    this.trees,
    this.updateProcessSeasonStatus,
    this.stages,
    this.loadDetailStatus,
    required this.actionWithStepStatus,
  });

  ProcessSeasonState copyWith({
    String? name,
    List<TreeEntity>? trees,
    LoadStatus? updateProcessSeasonStatus,
    LoadStatus? loadDetailStatus,
    List<StageEntity>? stages,
    int? actionWithStepStatus,
  }) {
    return ProcessSeasonState(
        name: name ?? this.name,
        trees: trees ?? this.trees,
        updateProcessSeasonStatus:
            updateProcessSeasonStatus ?? this.updateProcessSeasonStatus,
        loadDetailStatus: loadDetailStatus ?? this.loadDetailStatus,
        stages: stages ?? this.stages,
        actionWithStepStatus:
            actionWithStepStatus ?? this.actionWithStepStatus);
  }

  @override
  List<Object?> get props => [
        this.name,
        this.trees,
        this.updateProcessSeasonStatus,
        this.stages,
        this.loadDetailStatus,
        actionWithStepStatus
      ];
}
