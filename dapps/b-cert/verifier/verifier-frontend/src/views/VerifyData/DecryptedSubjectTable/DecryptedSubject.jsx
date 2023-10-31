import React from "react";
import DecryptedVersion from "./DecryptedVersion";

export default function DecryptedSubject({ subject, subjectIndex }) {
  return (
    <>
      {subject.versions.map((version, versionIndex) => (
        <DecryptedVersion {...{ subjectIndex, version, versionIndex }} key={versionIndex}></DecryptedVersion>
      ))}
    </>
  );
}
