/**
 * letsrolld API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { RequestFile } from './models';
import { DirectorFilmsInner } from './directorFilmsInner';
import { DirectorInfo } from './directorInfo';

export class Director {
    'info': DirectorInfo;
    'films'?: Array<DirectorFilmsInner>;

    static discriminator: string | undefined = undefined;

    static attributeTypeMap: Array<{name: string, baseName: string, type: string}> = [
        {
            "name": "info",
            "baseName": "info",
            "type": "DirectorInfo"
        },
        {
            "name": "films",
            "baseName": "films",
            "type": "Array<DirectorFilmsInner>"
        }    ];

    static getAttributeTypeMap() {
        return Director.attributeTypeMap;
    }
}

