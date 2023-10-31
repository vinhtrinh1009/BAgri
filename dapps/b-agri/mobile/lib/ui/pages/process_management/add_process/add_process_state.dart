part of 'add_process_cubit.dart';

class AddProcessState extends Equatable {
  final String? name;
  final LoadStatus? addProcessStatus;
  final List<TreeEntity>? trees;
  final List<TaskEntity>? listTask;

  final List<StageEntity>? stages;
  int actionWithStepStatus;
  AddProcessState({
    this.name,
    this.addProcessStatus,
    this.trees,
    this.listTask,
    this.stages,
    required this.actionWithStepStatus,
  });

  AddProcessState copyWith({
    String? name,
    LoadStatus? addProcessStatus,
    List<TreeEntity>? trees,
    List<TaskEntity>? listTask,
    List<StageEntity>? stages,
    int? actionWithStepStatus,
  }) {
    return AddProcessState(
        name: name ?? this.name,
        addProcessStatus: addProcessStatus ?? this.addProcessStatus,
        trees: trees ?? this.trees,
        listTask: listTask ?? this.listTask,
        stages: stages ?? this.stages,
        actionWithStepStatus:
            actionWithStepStatus ?? this.actionWithStepStatus);
  }

  @override
  List<Object?> get props => [
        this.name,
        this.trees,
        this.addProcessStatus,
        this.listTask,
        this.stages,
        actionWithStepStatus,
      ];
}
