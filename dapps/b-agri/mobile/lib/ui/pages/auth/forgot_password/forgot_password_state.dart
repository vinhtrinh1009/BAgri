part of 'forgot_password_cubit.dart';

class ForgotPasswordState extends Equatable {
  LoadStatus? loadStatus;

  @override
  List<Object?> get props => [
        this.loadStatus,
      ];

  ForgotPasswordState({
    this.loadStatus,
  });

  ForgotPasswordState copyWith({
    LoadStatus? loadStatus,
  }) {
    return ForgotPasswordState(
      loadStatus: loadStatus ?? this.loadStatus,
    );
  }
}
