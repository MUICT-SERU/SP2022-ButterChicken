import * as vscode from "vscode";
import fetch from "node-fetch";
import { IPreProcessResponse, IResponse, TyphonModel } from "./interfaces";

export function runTyphon({
  isPreProcessed,
  isSideFeature,
  mlSupport,
}: {
  isPreProcessed?: boolean;
  isSideFeature?: boolean;
  mlSupport?: boolean;
}) {
  const externsionConfig = vscode.workspace.getConfiguration("typhon");
  const searchModel = externsionConfig.get("model");
  const isBM25 = searchModel === TyphonModel.BM25;

  // Handle not support ML
  if (!isBM25 && !mlSupport) {
    const message = "This Typhon command not support ML model.";
    const options = {
      modal: true,
      detail: "Please change Typhon model to BM25 in settings.",
    };
    vscode.window.showWarningMessage(message, options);
    return;
  }

  vscode.commands.executeCommand("editor.action.selectAll").then(async () => {
    const notebookEditor = vscode.window.activeNotebookEditor;

    if (notebookEditor) {
      const currentNotebook = notebookEditor.notebook;
      const currentSelectionIndex = notebookEditor.selection.start;

      const currentCell = currentNotebook.cellAt(currentSelectionIndex);

      if (currentCell.kind === vscode.NotebookCellKind.Markup) {
        // prepare data
        let markdownDesc = currentCell.document.getText();

        isBM25
          ? _runBM25Typhon({ markdownDesc, isPreProcessed, isSideFeature })
          : _runMLTyphon({ markdownDesc, isSideFeature });

        vscode.window.showInformationMessage(
          `Typhon is actived!\n(Model: ${searchModel})`
        );
      }
    }
  });
}

async function _runBM25Typhon({
  markdownDesc,
  isPreProcessed,
  isSideFeature,
}: {
  markdownDesc: string;
  isPreProcessed?: boolean;
  isSideFeature?: boolean;
}) {
  // API URLs
  // TODO: move to env
  const preprocessedUrl = "http://202.151.182.232/preprocess/";
  const url = "http://typhon-server.th1.proen.cloud/api/v1/ir";

  // pre process markdown
  if (isPreProcessed) {
    const preProcessedRes = await await fetch(preprocessedUrl, {
      method: "POST",
      headers: {
        // eslint-disable-next-line @typescript-eslint/naming-convention
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ markdown: [markdownDesc] }),
    });
    if (preProcessedRes.status !== 200) {
      vscode.window.showErrorMessage("Preprocessing markdown failed.");
      return;
    }
    const preProcessJson =
      (await preProcessedRes.json()) as IPreProcessResponse;
    markdownDesc = preProcessJson.preprocessed_markdown[0];
  }

  // send to middle API
  const response = (await (
    await fetch(isPreProcessed ? url + "/preprocess" : url + "/base", {
      method: "POST",
      headers: {
        // eslint-disable-next-line @typescript-eslint/naming-convention
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: markdownDesc }),
    })
  ));
  if (response.status !== 200) {
    vscode.window.showErrorMessage("Server Error!");
    return;
  }
  const responseJson = (await response.json()) as IResponse;

  if (!responseJson.error && responseJson.data) {
    const data = responseJson.data;
    if (data.totalHits === 0) {
      const message = "No result found.";
      const options = {
        modal: true,
        detail: "Please try again with another markdown description.",
      };
      vscode.window.showErrorMessage(message, options);
      return;
    }
    if (!isSideFeature) {
      vscode.commands
        .executeCommand("notebook.cell.insertCodeCellBelowAndFocusContainer")
        .then(() => {
          vscode.commands.executeCommand("editor.action.selectAll").then(() => {
            const editor = vscode.window.activeTextEditor;
            if (editor) {
              editor.edit((editBuilder) => {
                editBuilder.insert(editor.selection.active, data.hits[0].code);
              });
            }
          });
        });
    } else {
      const header = `Typhon Result (${data.hits.length} results)`;
      const divider = `\n\n=====================\n\n`;
      const content = data.hits.reduce(
        (acc, hit) => acc + hit.code + divider,
        header + divider
      );

      vscode.commands.executeCommand(
        "notebook.cell.insertCodeCellBelowAndFocusContainer"
      );
      const document = await vscode.workspace.openTextDocument({
        language: "python",
        content,
      });
      vscode.window.showTextDocument(document, vscode.ViewColumn.Beside, true);
    }
  }
  else {
    vscode.window.showErrorMessage(responseJson.error || 'Data does not exist!');
  }
}

async function _runMLTyphon({
  markdownDesc,
  isSideFeature,
}: {
  markdownDesc: string;
  isSideFeature?: boolean;
}) {
  // TODO: Integrate with ML API
}
