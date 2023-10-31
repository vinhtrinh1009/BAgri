part of 'update_process_cubit.dart';

class UpdateProcessState extends Equatable {
  final String? name;
  final LoadStatus? updateProcessStatus;
  final List<TreeEntity>? trees;
  final List<TaskEntity>? listTask;
  final List<StageEntity>? stages;
  final LoadStatus? loadDetailStatus;
  int actionWithStepStatus;

  UpdateProcessState({
    this.name,
    this.trees,
    this.updateProcessStatus,
    this.listTask,
    this.stages,
    this.loadDetailStatus,
    required this.actionWithStepStatus,
  });

  UpdateProcessState copyWith({
    String? name,
    List<TreeEntity>? trees,
    LoadStatus? updateProcessStatus,
    List<TaskEntity>? listTask,
    LoadStatus? loadDetailStatus,
    List<StageEntity>? stages,
    int? actionWithStepStatus,
  }) {
    return UpdateProcessState(
        name: name ?? this.name,
        trees: trees ?? this.trees,
        updateProcessStatus: updateProcessStatus ?? this.updateProcessStatus,
        listTask: listTask ?? this.listTask,
        loadDetailStatus: loadDetailStatus ?? this.loadDetailStatus,
        stages: stages ?? this.stages,
        actionWithStepStatus:
            actionWithStepStatus ?? this.actionWithStepStatus);
  }

  @override
  List<Object?> get props => [
        this.name,
        this.trees,
        this.updateProcessStatus,
        this.listTask,
        this.stages,
        this.loadDetailStatus,
        actionWithStepStatus
      ];
}
