/* eslint-disable @typescript-eslint/naming-convention */
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import fetch from 'node-fetch';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	console.log("Typhon extension activated");
 
	context.subscriptions.push(
		vscode.commands.registerCommand('typhon.test', () => {
			// vscode.commands.executeCommand('editor.action.selectAll').then(async () => {});
			const editor = vscode.window.activeTextEditor;
			if (editor) {
				editor.edit((editBuilder) => {
					editBuilder.insert(editor.selection.active, 'Hello World!');
				});
			}
		})
	);

	context.subscriptions.push(
		vscode.commands.registerCommand('typhon.run', () => {
			vscode.commands.executeCommand('editor.action.selectAll').then(async () => {
				const notebookEditor = vscode.window.activeNotebookEditor;
				
				if (notebookEditor) {
					const currentNotebook = notebookEditor.notebook;
					const currentSelectionIndex = notebookEditor.selection.start;

					const currentCell = currentNotebook.cellAt(currentSelectionIndex);
					
					if (currentCell.kind === vscode.NotebookCellKind.Markup) {

						// prepare data
						const markdownDesc = currentCell.document.getText();

						// send to middle API
						const url = 'http://typhon-server.th1.proen.cloud/api/v1/ir';
						const response = await (await fetch(url, {
							method: 'POST',
							headers: {
      					'Content-Type': 'application/json'
							},
							body: JSON.stringify({ query: markdownDesc }),
						})).json() as IResponse;

						console.log(response);
						if (!response.error && response.data) {
							const data = response.data;

							vscode.window.showInformationMessage('Typhon is actived!');
							vscode.commands.executeCommand('notebook.cell.insertCodeCellBelowAndFocusContainer').then(() => {
								vscode.commands.executeCommand('editor.action.selectAll').then(() => {
									const editor = vscode.window.activeTextEditor;
									if (editor) {
										editor.edit((editBuilder) => {
											editBuilder.insert(editor.selection.active, data.hits[0].code);
										});
									}
								});
							});
						}
					}
				}

			});
		}
	));
}

// This method is called when your extension is deactivated
export function deactivate() {}

interface BM25Props {
	code: string;
	score: number;
}
interface IResponse {
	error?: string;
	data?: {
		totalHits: number;
		hits: BM25Props[];
	};
}
